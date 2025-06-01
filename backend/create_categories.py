from news.models import Category

# List of categories to create
categories = [
    {
        'name': 'Technology',
        'description': 'Latest news in tech, gadgets, and digital innovation'
    },
    {
        'name': 'Business',
        'description': 'Business news, market updates, and economic trends'
    },
    {
        'name': 'Science',
        'description': 'Scientific discoveries, research, and breakthroughs'
    },
    {
        'name': 'Health',
        'description': 'Health news, medical research, and wellness updates'
    },
    {
        'name': 'Entertainment',
        'description': 'Movies, music, TV shows, and celebrity news'
    },
    {
        'name': 'Sports',
        'description': 'Sports news, scores, and athlete updates'
    },
    {
        'name': 'Politics',
        'description': 'Political news, policy changes, and government updates'
    },
    {
        'name': 'Environment',
        'description': 'Environmental news, climate change, and sustainability'
    },
    {
        'name': 'Education',
        'description': 'Education news, academic research, and learning trends'
    },
    {
        'name': 'World',
        'description': 'International news and global events'
    }
]

# Create categories
for category_data in categories:
    Category.objects.get_or_create(
        name=category_data['name'],
        defaults={'description': category_data['description']}
    )

print("Categories created successfully!") 