import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

# ─── إعدادات البوت ───────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

RULES_FILE = "rules.json"

# ─── تحميل القوانين ───────────────────────────────────────────────
def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "general": {
            "title_ar": "📋 القوانين العامة",
            "title_en": "📋 General Rules",
            "color": 0x2ECC71,
            "emoji": "📋",
            "rules_ar": [
                "🔇 **الاحترام المتبادل** — يُمنع السب أو الإهانة بأي شكل.",
                "🚫 **لا للسبام** — ممنوع تكرار الرسائل أو الفلود.",
                "🔞 **محتوى مناسب** — يُمنع نشر محتوى +18 خارج القنوات المخصصة.",
                "📢 **لا للإعلانات** — ممنوع الإعلان بدون إذن.",
            ],
            "rules_en": [
                "🔇 **Mutual Respect** — No insults or harassment.",
                "🚫 **No Spam** — No flooding or repeated messages.",
                "🔞 **Appropriate Content** — No +18 content outside designated channels.",
                "📢 **No Ads** — No advertising without permission.",
            ]
        },
        "crimes": {
            "title_ar": "⚔️ قوانين الإجرام",
            "title_en": "⚔️ Crime Rules",
            "color": 0xE74C3C,
            "emoji": "⚔️",
            "rules_ar": [
                "🔫 **السرقة** — يُمنع السرقة خارج المناطق المحددة.",
                "💰 **الابتزاز** — يُمنع ابتزاز اللاعبين تحت أي ظرف.",
                "🚗 **سرقة السيارات** — مسموح فقط في المناطق الحمراء.",
                "⚠️ **الاشتباكات** — يجب الالتزام بقواعد RP أثناء الاشتباكات.",
            ],
            "rules_en": [
                "🔫 **Robbery** — No robbing outside designated zones.",
                "💰 **Extortion** — No extorting players under any circumstance.",
                "🚗 **Car Theft** — Only allowed in red zones.",
                "⚠️ **Fights** — Must follow RP rules during all confrontations.",
            ]
        },
        "zones": {
            "title_ar": "🛡️ المناطق الأمنة",
            "title_en": "🛡️ Safe Zones",
            "color": 0x3498DB,
            "emoji": "🛡️",
            "rules_ar": [
                "🏥 **المستشفى** — منطقة آمنة بالكامل، يُمنع الاشتباك.",
                "🏦 **البنك** — ممنوع التعدي داخل المنطقة الآمنة للبنك.",
                "🚓 **مركز الشرطة** — منطقة آمنة كاملة للمدنيين.",
                "🏪 **المتاجر الحكومية** — يُمنع أي نشاط إجرامي بمحيطها.",
            ],
            "rules_en": [
                "🏥 **Hospital** — Fully safe zone, no combat allowed.",
                "🏦 **Bank** — No aggression inside the bank safe area.",
                "🚓 **Police Station** — Full safe zone for civilians.",
                "🏪 **Gov Shops** — No criminal activity in their vicinity.",
            ]
        },
        "discord": {
            "title_ar": "💬 قوانين ديسكورد",
            "title_en": "💬 Discord Rules",
            "color": 0x9B59B6,
            "emoji": "💬",
            "rules_ar": [
                "🎙️ **الفويس** — يُمنع الإزعاج أو رفع الصوت بشكل مبالغ.",
                "📝 **التشات** — استخدم القنوات الصحيحة لكل موضوع.",
                "🤖 **البوتات** — استخدم البوتات في قناتها المخصصة فقط.",
                "🏷️ **الإشارات** — يُمنع منشن الإدارة بدون سبب.",
            ],
            "rules_en": [
                "🎙️ **Voice** — No excessive noise or screaming.",
                "📝 **Chat** — Use the correct channels for each topic.",
                "🤖 **Bots** — Use bots only in their designated channel.",
                "🏷️ **Mentions** — Do not mention staff without a valid reason.",
            ]
        },
        "last_updated": datetime.now().isoformat(),
        "notify_channel_id": None,
        "server_name": "السيرفر",
        "server_logo": None
    }

def save_rules(data):
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

CATEGORIES = ["general", "crimes", "zones", "discord"]

def build_category_embed(rules_data, category_key, lang="ar"):
    cat = rules_data[category_key]
    title = cat["title_ar"] if lang == "ar" else cat["title_en"]
    rules_list = cat["rules_ar"] if lang == "ar" else cat["rules_en"]
    embed = discord.Embed(
        title=title,
        description="\n\n".join(rules_list),
        color=cat["color"],
        timestamp=datetime.now()
    )
    server_name = rules_data.get("server_name", "السيرفر")
    embed.set_footer(text=f"{server_name} • جميع الحقوق محفوظة ©")
    logo = rules_data.get("server_logo")
    if logo:
        embed.set_thumbnail(url=logo)
    return embed

CATEGORY_LABELS = {
    "general": ("📋 القوانين العامة", "General Rules"),
    "crimes":  ("⚔️ قوانين الإجرام",  "Crime Rules"),
    "zones":   ("🛡️ المناطق الأمنة",  "Safe Zones"),
    "discord": ("💬 قوانين ديسكورد",  "Discord Rules"),
}

# ─── القائمة المنسدلة ─────────────────────────────────────────────
class RulesSelect(discord.ui.Select):
    def __init__(self, lang="ar"):
        self.lang = lang
        options = [
            discord.SelectOption(
                label=label_ar if lang == "ar" else label_en,
                value=key
            )
            for key, (label_ar, label_en) in CATEGORY_LABELS.items()
        ]
        super().__init__(
            placeholder="...اختر نوع القوانين" if lang == "ar" else "Select rule category...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"rules_select_{lang}"
        )

    async def callback(self, interaction: discord.Interaction):
        rules_data = load_rules()
        embed = build_category_embed(rules_data, self.values[0], self.lang)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class RulesView(discord.ui.View):
    def __init__(self, lang="ar"):
        super().__init__(timeout=None)
        self.lang = lang
        self.add_item(RulesSelect(lang=lang))

    @discord.ui.button(
        label="✖ إغلاق",
        style=discord.ButtonStyle.danger,
        custom_id="close_rules_btn"
    )
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.delete()
        except Exception:
            pass
        await interaction.response.send_message("تم إغلاق القوانين ✅", ephemeral=True)


def build_main_embed(rules_data):
    server_name = rules_data.get("server_name", "السيرفر")
    embed = discord.Embed(
        title=f"جميع القوانين الخاصة بـ {server_name}",
        description="يرجوا منك إتباع جميع القوانين لكي لا يتم محاسبتك",
        color=0x1ABC9C
    )
    logo = rules_data.get("server_logo")
    if logo:
        embed.set_image(url=logo)
    embed.set_footer(text=f"{server_name} • جميع الحقوق محفوظة ©")
    return embed


@bot.event
async def on_ready():
    await tree.sync()
    bot.add_view(RulesView(lang="ar"))
    bot.add_view(RulesView(lang="en"))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="قوانين السيرفر 📜"
        )
    )
    print(f"✅ البوت شغال: {bot.user} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")


@tree.command(name="قوانين", description="إرسال رسالة القوانين التفاعلية (إدارة)")
@app_commands.checks.has_permissions(administrator=True)
async def send_rules(interaction: discord.Interaction):
    rules_data = load_rules()
    embed = build_main_embed(rules_data)
    await interaction.response.send_message(embed=embed, view=RulesView(lang="ar"))


@tree.command(name="rules", description="Send interactive rules message in English (admin)")
@app_commands.checks.has_permissions(administrator=True)
async def send_rules_en(interaction: discord.Interaction):
    rules_data = load_rules()
    embed = build_main_embed(rules_data)
    await interaction.response.send_message(embed=embed, view=RulesView(lang="en"))


@tree.command(name="setname", description="ضبط اسم السيرفر في القوانين (إدارة)")
@app_commands.describe(name="اسم السيرفر")
@app_commands.checks.has_permissions(administrator=True)
async def set_name(interaction: discord.Interaction, name: str):
    rules_data = load_rules()
    rules_data["server_name"] = name
    save_rules(rules_data)
    await interaction.response.send_message(f"✅ تم ضبط الاسم: **{name}**", ephemeral=True)


@tree.command(name="setlogo", description="ضبط لوجو السيرفر (رابط صورة) (إدارة)")
@app_commands.describe(url="رابط الصورة")
@app_commands.checks.has_permissions(administrator=True)
async def set_logo(interaction: discord.Interaction, url: str):
    rules_data = load_rules()
    rules_data["server_logo"] = url
    save_rules(rules_data)
    await interaction.response.send_message("✅ تم ضبط اللوجو!", ephemeral=True)


@tree.command(name="updaterule", description="تعديل قانون معين (إدارة)")
@app_commands.describe(
    category="الفئة: general / crimes / zones / discord",
    lang="اللغة: ar أو en",
    rule_number="رقم القانون",
    new_text="النص الجديد"
)
@app_commands.checks.has_permissions(administrator=True)
async def update_rule(interaction: discord.Interaction, category: str, lang: str, rule_number: int, new_text: str):
    rules_data = load_rules()
    if category not in CATEGORIES:
        await interaction.response.send_message("❌ فئة غير صحيحة.", ephemeral=True)
        return
    key = f"rules_{lang}"
    rules_list = rules_data[category].get(key, [])
    if rule_number < 1 or rule_number > len(rules_list):
        await interaction.response.send_message(f"❌ الرقم يجب يكون بين 1 و {len(rules_list)}", ephemeral=True)
        return
    rules_data[category][key][rule_number - 1] = new_text
    rules_data["last_updated"] = datetime.now().isoformat()
    save_rules(rules_data)
    notify_id = rules_data.get("notify_channel_id")
    if notify_id:
        channel = bot.get_channel(int(notify_id))
        if channel:
            e = discord.Embed(title="⚠️ تم تحديث القوانين!", color=0xE74C3C, timestamp=datetime.now())
            e.add_field(name="الفئة", value=f"{category} ({lang.upper()})", inline=True)
            e.add_field(name="رقم القانون", value=str(rule_number), inline=True)
            e.add_field(name="النص الجديد", value=new_text, inline=False)
            e.set_footer(text=f"بواسطة: {interaction.user.display_name}")
            await channel.send(embed=e)
    await interaction.response.send_message("✅ تم التحديث!", ephemeral=True)


@tree.command(name="setchannel", description="ضبط قناة إشعارات تحديث القوانين (إدارة)")
@app_commands.describe(channel="القناة")
@app_commands.checks.has_permissions(administrator=True)
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    rules_data = load_rules()
    rules_data["notify_channel_id"] = str(channel.id)
    save_rules(rules_data)
    await interaction.response.send_message(f"✅ قناة الإشعارات: {channel.mention}", ephemeral=True)


@bot.event
async def on_member_join(member: discord.Member):
    welcome_channel = None
    for ch in member.guild.text_channels:
        if any(w in ch.name.lower() for w in ["welcome", "ترحيب", "general", "عام"]):
            welcome_channel = ch
            break
    if welcome_channel:
        embed = discord.Embed(
            title=f"👋 مرحباً {member.display_name}!",
            description=(
                f"يسعدنا انضمامك لـ **{member.guild.name}**!\n\n"
                "تأكد تقرأ قوانين السيرفر باستخدام `/قوانين`"
            ),
            color=0x2ECC71
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await welcome_channel.send(embed=embed)


@send_rules.error
@send_rules_en.error
@update_rule.error
@set_channel.error
@set_name.error
@set_logo.error
async def permission_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ ما عندك صلاحية!", ephemeral=True)


if not TOKEN:
    print("❌ خطأ: ما لقيت DISCORD_TOKEN في متغيرات البيئة!")
    exit(1)

bot.run(TOKEN)
