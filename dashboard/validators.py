def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    print "In validator function"
    print ext, value
    valid_extensions = ['.zip', '.tar', '.tar.gz', '.gz']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension. Upload only .zip, .tar.gz, .gz, .tar files only')
