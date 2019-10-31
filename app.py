#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    WSGI APP to convert wkhtmltopdf As a webservice
    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import tempfile
import zipfile
from werkzeug.wsgi import wrap_file
from werkzeug.wrappers import Request, Response
from executor import execute


@Request.application
def application(request):
    """
    To use this application, the user must send a POST request with
    base64 or form encoded encoded HTML content and the wkhtmltopdf Options in
    request data, with keys 'base64_html' and 'options'.
    The application will return a response with the PDF file.
    """
    if request.method != 'POST':
        return Response('alive')

    with tempfile.NamedTemporaryFile(suffix='.zip') as source_file:
        source_file.write(request.files['file'].read())

        source_file.flush()

        with tempfile.TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(source_file.name, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)

                args = ['pdfunite']

                for file_name in zip_ref.namelist():
                    args += [tmpdirname + file_name]

                output_file = tmpdirname + '/output.pdf'
                args += [output_file]

                cmd = ' '.join(args)

                execute(cmd)

                pdf_file = open(output_file)

                return Response(
                    wrap_file(request.environ, pdf_file),
                    mimetype='application/pdf',
                    direct_passthrough=True,
                )


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, application, use_debugger=True, use_reloader=True
    )
