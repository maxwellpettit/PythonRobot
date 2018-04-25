import asyncio, evdev

xbox = evdev.InputDevice('/dev/input/event0')

print(xbox.capabilities(verbose=True))

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')
        print(event)

asyncio.ensure_future(print_events(xbox))

loop = asyncio.get_event_loop()
loop.run_forever()
