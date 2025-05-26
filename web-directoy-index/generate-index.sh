#!/bin/bash

TARGET_DIR="/var/www/html/software"
OUTPUT_FILE="$TARGET_DIR/index.html"

# HTML Header
cat <<EOF > "$OUTPUT_FILE"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Software Downloads</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
    <h1 class="mb-4">Software Downloads</h1>
    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>File Name</th>
                <th>Size</th>
                <th>Last Modified</th>
            </tr>
        </thead>
        <tbody>
EOF

# Loop through files
for file in "$TARGET_DIR"/*; do
    [ -f "$file" ] || continue
    filename=$(basename "$file")
    filesize=$(du -h "$file" | cut -f1)
    lastmod=$(date -r "$file" "+%Y-%m-%d %H:%M")
    echo "        <tr>
                <td><a href=\"$filename\">$filename</a></td>
                <td>$filesize</td>
                <td>$lastmod</td>
            </tr>" >> "$OUTPUT_FILE"
done

# HTML Footer
cat <<EOF >> "$OUTPUT_FILE"
        </tbody>
    </table>
</div>
</body>
</html>
EOF

echo "✅ HTML index generated at $OUTPUT_FILE"
