import zipfile, os 

def create_archive(path='./test/'): 
    '''Create the ZIP archive.  The mimetype must be the first file in the archive 
    and it must not be compressed.''' 

    epub_name = "test.epub" 

    # The EPUB must contain the META-INF and mimetype files at the root, so 
    # we'll create the archive in the working directory first and move it later     
    epub = zipfile.ZipFile(epub_name, 'w') 
    os.chdir(path)
    # Open a new zipfile for writing 

    # Add the mimetype file first and set it to be uncompressed 
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED) 
    
    # For the remaining paths in the EPUB, add all of their files 
    # using normal ZIP compression 
    for i in os.listdir('.'):
        if os.path.isdir(i):
            for j in os.listdir(i):
                epub.write(i + '/' + j, compress_type=zipfile.ZIP_DEFLATED)
    epub.close()

create_archive()