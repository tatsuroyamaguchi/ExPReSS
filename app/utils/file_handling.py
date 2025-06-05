import io
import zipfile

def create_zip_file(json_name, output_stream, proteinpaint_path, disco_path):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(json_name + '.xlsx', output_stream.getvalue())
        with open(proteinpaint_path, 'rb') as f:
            zip_file.writestr(json_name + 'proteinpaint.tsv', f.read())
        with open(disco_path, 'rb') as f:
            zip_file.writestr(json_name + 'disco.tsv', f.read())
    zip_buffer.seek(0)
    return zip_buffer