    @commands.command(
        brief=
        'This command can be used to login your account.',
        description=
        'This command can be used to approve a user to bypass vote-only commands.',
        usage="@member")
    @commands.dm_only()
    @commands.check_any(is_bot_staff())
    @commands.dm_only()
    async def loginDeveloper(self, ctx):
      