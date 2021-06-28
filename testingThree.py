    @commands.command(
        brief=
        'This command can be used to login into developer account.',
        description=
        'This command can be used to login your developer account.',
        usage="")
    @commands.dm_only()
    @commands.check_any(is_bot_staff())
    async def loginDeveloper(self, ctx,*,password):
      global restrictedUsers
      if password=='123':
        await ctx.send(" You have been permitted to developer permissions in this bot for an hour .")
        botowners.append(ctx.author.id)
        start_time = time.time()
        while(ctx.author.status==discord.Status.online and int(time.time() - start_time)<=1800):
          pass 
        botowners.remove(ctx.author.id)
      else:
        await ctx.send(" You have been restricted access from this bot for 30 minutes .")
        restrictedUsers.append(str(ctx.author.id))
        await asyncio.sleep(1800)
        restrictedUsers.remove(str(ctx.author.id))
      
