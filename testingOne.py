async def func(ctx,id):
    user=await client.fetch_user(id)
    embed = discord.Embed(title="User Profile", description="\u200b", color=Color.green())
    embed.add_field(name='Username',value=user.name)
    embed.add_field(name='User-id',value=user.id)
    embed.add_field(name='User-discriminator',value=user.discriminator)
    userflag=user.public_flags
    strflag=""
    if userflag.staff:
      strflag+="Discord staff ,"
    if userflag.partner:
      strflag+="Discord partner ,"
    if userflag.hypesquad:
      strflag+="Hypesquad event ,"
    if userflag.bug_hunter:
      strflag+="Discord bug hunter ,"
    if userflag.hypesquad_bravery:
      strflag+="HypeSquad Bravery ,"
    if userflag.hypesquad_brilliance:
      strflag+="HypeSquad Brilliance ,"
    if userflag.hypesquad_balance:
      strflag+="HypeSquad Balance ,"
    if userflag.early_supporter:
      strflag+="Early Supporter ,"
    if userflag.team_user:
      strflag+="Team User ,"
    if userflag.system:
      strflag+="Official discord ,"
    if userflag.bug_hunter_level_2:
      strflag+="Bug Hunter Level 2 ,"
    if userflag.verified_bot:
      strflag+="Verified bot ,"
    if userflag.verified_bot_developer:
      strflag+="Early Verified Bot Developer ,"
    original_string=strflag
    print(original_string)
    last_char_index = original_string.rfind(",")
    new_string = original_string[:last_char_index] + "." + original_string[last_char_index+1:]
    embed.add_field(name='User-flags',value=new_string)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)
client.loop.create_task(func(ctx,488643992628494347))