from discord import VoiceRegion, Embed
from config import version
bot_invite = "https://discord.com/api/oauth2/authorize?client_id=717731069977165905&permissions=268438656&scope=bot"
guild_invite = "https://discord.gg/ZDn4GVj"
color = 0x00bfff


class LangMessage:
    def __init__(self, guild):
        self.lang = 1
        if guild is None:
            return
        if guild.region == VoiceRegion.japan:
            self.lang = 2

    def greeting_embed_ja(self):
        embed = Embed(title='導入してくださりありがとうございます！',
                      description='\nこのBotの簡単な説明をさせていただきます。\n詳細な情報は`khelp`コマンドからご確認ください。',
                      color=color)
        embed.add_field(name='機能',
                        value='このBotは、サーバーから退出したユーザーが再入室した際、退出する前に持っていた役職を自動付与するBotです。\n'
                              'このBotに付与されている、`Role Keeper`という名前の役職よりも下にある役職にのみ有効です。',
                        inline=False
                        )
        embed.add_field(name='招待など',
                        value=f"[Botの招待URL]({bot_invite})\n"
                              f"[Botの公式サーバー]({guild_invite})",
                        inline=False
                        )
        return embed

    def greeting_embed_en(self):
        embed = Embed(title="Thank you so much for the introduction!\n"
                            "For more information, please use the `khelp` command.",
                      description="Let me give you a brief description of this bot.",
                      color=color)
        embed.add_field(name="Features",
                        value="This Bot is a bot that automatically grants a user who has left the server"
                              " the position they held before leaving when they rejoin the server. \n"
                              "It is only valid for positions below the position named `Role Keeper`"
                              " that are granted to this Bot.",
                        inline=False
                        )
        embed.add_field(name='Invitations',
                        value=f"[Bot invite]({bot_invite})\n"
                              f"[Bot's guild]({guild_invite})",
                        inline=False
                        )
        return embed

    @property
    def greeting_embed(self):
        if self.lang == 2:
            embed = self.greeting_embed_ja()
        else:
            embed = self.greeting_embed_en()

        embed.add_field(name='Language/言語',
                        value='If you have set your voice region to Japan, all explanations will be in Japanese.'
                              ' Otherwise, it will be in English.\n'
                              'ボイスリージョンを日本にしている場合、説明が全て日本語になります。それ以外の場合、英語になります。',
                        inline=False
                        )

        return embed

    def help_embed_ja(self):
        embed = Embed(title=f"Role Keeper v{version} Help",
                      description="Role Keeperの使い方を説明します",
                      color=color
                      )
        embed.add_field(name="仕組みについて",
                        value="このBotは、サーバーから退出したユーザーが再入室した際、退出する前に持っていた役職を自動付与するBotです。\n"
                        "このBotに付与されている、`Role Keeper`という名前の役職よりも下にある役職にのみ有効です。\n"
                        "もし間違って消してしまった場合は、Role Keeperという名前の役職を作り、役職管理権限を付与してください。",
                        inline=False
                        )
        embed.add_field(name="コマンド一覧",
                        value="設定に必要なコマンド一覧を表示します\n"
                              "コマンドはありません。",
                        inline=False
                        )
        return embed

    def help_embed_en(self):
        embed = Embed(title=f"Role Keeper v{version} Help",
                      description="Show how to use Role Keeper",
                      color=color
                      )
        embed.add_field(name="Features",
                        value="This Bot is a bot that automatically grants a user who has left the server"
                              " the position they held before leaving when they rejoin the server. \n"
                              "It is only valid for positions below the position named `Role Keeper`"
                              " that are granted to this Bot.\n"
                              "If you accidentally erased it,\n"
                              " please create a role named Role Keeper and give it `manage roles` permission.",
                        inline=False
                        )
        embed.add_field(name="Commands",
                        value="Displays a list of commands required for the setting.\n"
                              "No commands.",
                        inline=False
                        )
        return embed

    @property
    def help_embed(self):
        if self.lang == 2:
            embed = self.help_embed_ja()
        else:
            embed = self.help_embed_en()
        embed.add_field(name='Language/言語',
                        value='If you have set your voice region to Japan, all explanations will be in Japanese.'
                              ' Otherwise, it will be in English.\n'
                              'ボイスリージョンを日本にしている場合、説明が全て日本語になります。それ以外の場合、英語になります。',
                        inline=False
                        )
        return embed

    def create_not_enough_message(self, not_enough):
        if self.lang == 2:
            text = "申し訳ありませんが、以下の権限がないため表示及び動作をすることができませんでした。\n{}"
        else:
            text = "We're sorry, " \
                   "but we couldn't display or operate because we don't have the following permissions:\n{}"

        return text.format("\n".join(not_enough))
