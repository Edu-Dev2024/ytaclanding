import json
from django.shortcuts import render
from django.templatetags.static import static


def landing_home(request):

    competitions = [
            {
                'title': "YTAC 2022",
                'location': "Imperial College, Kuala Lumpur, MY",
                'prize_pool': "$10,000",
                'description': "Our annual spring championship featuring multiple categories and exciting competitions. Athletes from across the region competed in various disciplines.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2022",
                'location': "Nanyang Technology University, SG",
                'prize_pool': "$25,000",
                'description': "High-stakes qualifying rounds for the summer olympics. Only the best athletes advanced to represent their countries.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2022",
                'location': "Southern University College, Johor, MY",
                'prize_pool': "$15,000",
                'description': "Multi-sport challenge event featuring team competitions and individual achievements in a festival atmosphere.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2022",
                'location': "Bangkok, TH",
                'prize_pool': "$12,000",
                'description': "Currently ongoing winter sports competition featuring indoor events and exciting matchups.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2022",
                'location': "Tech Dome, Pulau Pinang, MY",
                'prize_pool': "$30,000",
                'description': "The biggest competition of the year! Regional championship finals with the highest prize pool and prestige.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2023",
                'location': "Online mode, MY",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "ICIA 2023",
                'location': "Surabaya, ID",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2024",
                'location': "University Malaya, MY",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "ICIA 2024",
                'location': "King Mongkut's University of Technology Thonburi, Bangkok, TH",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "IITS 2024",
                'location': "China Millennium Monument, Beijing, CN",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2025",
                'location': "Kuching, MY",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "ICIA 2025",
                'location': "Ho Chi Minh City, VN",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "past",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "YTAC 2026",
                'location': "Tech Dome, Pulau Pinang, MY",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "future",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            },
            {
                'title': "ICIA 2026",
                'location': "MM",
                'prize_pool': "$50,000",
                'description': "International level competition bringing together the world's best athletes for an unforgettable tournament.",
                'status': "future",
                'image': "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&h=300&fit=crop"
            }
        ];
    
    image_list = [
        'adminhub/landings/74A6381.jpg',
        'adminhub/landings/74A6469.jpg',
        'adminhub/landings/74A6484.jpg',
        'adminhub/landings/74A6487.jpg',
        'adminhub/landings/74A8791.jpg',
        'adminhub/landings/74A9294.jpg',
        'adminhub/landings/2022 KL.jpg',
        'adminhub/landings/2022 Penang.jpg',
        'adminhub/landings/2022 Thailand.jpg',
        'adminhub/landings/2024 Bangkok.jpg',
        'adminhub/landings/2025 YTAC Kuching 2.jpg',
        'adminhub/landings/400086798_366143965931187_6028160454133792059_n.jpg',
        'adminhub/landings/470217011_578165304922022_7056793439237242767_n.jpg',
        'adminhub/landings/476874104_619186410819911_5700536684330393316_n.jpg',
        'adminhub/landings/480411911_660510496736007_2812944273093984792_n.jpg',
        'adminhub/landings/480411911_660510496736007_2812944273093984792_n.jpg',
        'adminhub/landings/481657878_671961708924219_4573594943700561803_n.jpg',
        'adminhub/landings/483882390_680781001375623_5581528199823005665_n.jpg',
        'adminhub/landings/484022434_680781101375613_8195342417301964991_n.jpg',
        'adminhub/landings/484037570_680781008042289_1840705236586775842_n.jpg',
        'adminhub/landings/Artboard 4.jpg',
        'adminhub/landings/Artboard 5.jpg',
        'adminhub/landings/Artboard 6.jpg',
        'adminhub/landings/IMG_7675.JPG',
        'adminhub/landings/WhatsApp Image 2025-06-04 at 02.01.06_4e984e1d.jpg',
    ]

    context = {
        'image_list': image_list,
        'competitions': competitions,
    }
    
    return render(request, 'adminhub/index.html', context)

def landing_ytac(request):


    return render(request, 'adminhub/info_ytac.html')

def landing_iitc(request):


    return render(request, 'adminhub/info_iitc.html')

def landing_icia(request):


    return render(request, 'adminhub/info_icia.html')