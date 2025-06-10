def format_movie_preview(title, year, rating):
    return f"🎬 <b>{title}</b> ({year})\n⭐️ {rating}\n\n📖 /details_{title.replace(' ', '_')}"
