gn!execcode
async def func(ctx):
  start_time=time.time() #taking current time as starting time
  await asyncio.sleep(5)
  #here your code

  elapsed_time=time.time()-start_time #again taking current time - starting time 
  await ctx.send(f" The elapsed time was {elapsed_time} .")
client.loop.create_task(func(ctx))