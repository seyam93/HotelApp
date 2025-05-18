from hotels.models import HotelVideoBanner, HotelPageBanner

def get_page_banner(hotel, page):
    video = HotelVideoBanner.objects.filter(hotel=hotel, page=page).first()
    if video and (video.video_file or video.video_url):
        return {'type': 'video', 'object': video}

    image = HotelPageBanner.objects.filter(hotel=hotel, page=page).first()
    if image:
        return {'type': 'image', 'object': image}

    return None  # No banner found