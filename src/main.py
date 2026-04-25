import asyncio
from loguru import logger
from brain.agent import axel

async def main():
    logger.info("⚡ AXEL READY sur nouveau Codespace...")
    prompt = "Mémorise que Flexbox s'active avec 'display: flex' en CSS, catégorie code."
    result = await axel.run(prompt)
    print(f"\n🤖 AXEL : {result.data}\n")

if __name__ == '__main__':
    asyncio.run(main())
