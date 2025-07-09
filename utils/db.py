from extractor_app.models import ExtractedContent

def store_content(content_type, data):
    if content_type == "image":
        ExtractedContent.objects.create(type=content_type, image=data)
    else:
        ExtractedContent.objects.create(type=content_type, content=data)
