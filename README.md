pdfunite Microservice
========================

Alpine container service for [pdfunite](https://poppler.freedesktop.org/).

## Usage

Run Container
```bash
docker run -d -p 29881:80 agilize/pdfunite
curl -X POST -vv -F 'file=@demo.zip' http://localhost:29881 -o demo.pdf
```

### PHP example

```php
<?php

/**
 * $files array
 * $output string
 */
function zip_files($files, $output) {
    // Initialize archive object
    $zip = new \ZipArchive();
    $zip->open($output, \ZipArchive::CREATE | \ZipArchive::OVERWRITE);

    foreach ($files as $index => $file)
    {
		// Add current file to archive
		$zip->addFile($file, \sprintf('/page%s.pdf', str_pad($index, 3, '0', STR_PAD_LEFT)));
    }

    // Zip archive will be created only after closing object
    $zip->close();
}

$files = [
	realpath('./demo/page4.pdf'),
	realpath('./demo/page1.pdf'),
	realpath('./demo/page2.pdf'),
	realpath('./demo/page3.pdf'),
];

$zipFilePath = tempnam('/tmp', 'demo') . '.zip';

zip_files($files, $zipFilePath);

// set request body
$data = [
    'file' => curl_file_create($zipFilePath),
];

// set header
$headers = [
];

// curl options
$options = [
    CURLOPT_URL            => 'http://localhost/',
    CURLOPT_PORT           => 29881,
    CURLOPT_POST           => 1,
    CURLOPT_POSTFIELDS     => $data,
    CURLOPT_HTTPHEADER     => $headers,
    CURLOPT_RETURNTRANSFER => true
];

// curl call
$ch = curl_init();
curl_setopt_array($ch, $options);
$result = curl_exec($ch);
curl_close($ch);

unlink($zipFilePath);

// print result
echo $result;
```
