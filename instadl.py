from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import instaloader

# Tokenni o'rnating
BOT_TOKEN = "7667712838:AAGm5s4DcshXKPgegFylXVeywsjxzDh2Ok0"

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Instaloader obyekti
insta_loader = instaloader.Instaloader()

# /start komandasini qayta ishlash
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salom! Instagram'dan video yuklash uchun post linkini yuboring.")

# Instagram video yuklash
@dp.message_handler()
async def download_instagram_video(message: types.Message):
    link = message.text
    if "instagram.com" not in link:
        await message.reply("Iltimos, to'g'ri Instagram post linkini yuboring.")
        return

    try:
        # Instagram postni yuklash
        post = instaloader.Post.from_shortcode(insta_loader.context, link.split("/")[-2])
        
        if post.is_video:
            video_url = post.video_url
            await message.reply("Video yuklanmoqda...")
            await bot.send_video(message.chat.id, video=video_url)
        else:
            await message.reply("Bu postda video yo'q, iltimos, boshqa link yuboring.")
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)