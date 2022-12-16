import os
import typer
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from gpt3_wordpress import Gpt3Wordpress

gpt3wordpress_cli = typer.Typer()


@gpt3wordpress_cli.command()
def cli(
        open_api_key: str = typer.Option(
            help="Your OpenAI API key.",
            envvar="OPENAI_API_KEY",
            default=os.getenv("OPENAI_API_KEY")
        ),
        wordpress_blog_url: str = typer.Option(
            help="Your WordPress blog URL. (e.g. https://example.com)",
            envvar="WORDPRESS_BLOG_URL",
            default=os.getenv("WORDPRESS_BLOG_URL")
        ),
        wordpress_username: str = typer.Option(
            help="Your WordPress username.",
            envvar="WORDPRESS_USERNAME",
            default=os.getenv("WORDPRESS_USERNAME")
        ),
        wordpress_password: str = typer.Option(
            help="Your WordPress password.",
            envvar="WORDPRESS_PASSWORD",
            default=os.getenv("WORDPRESS_PASSWORD")
        ),
        topic: str = typer.Option(
            ...,
            prompt="\nWhat is the topic of the post?",
            help="The topic of the post. (e.g. technology, crypto, ai, etc.)"
        ),
        tone: str = typer.Option(
            prompt="What is the tone of the post?",
            help="The tone of the post. (e.g. funny, serious, etc.)",
            default="neutral"
        ),
        max_words: int = typer.Option(
            prompt="Maximum words for the post?",
            help="Maximum words for the post. (e.g. 2500)",
            default=2500
        )
):
    generator = Gpt3Wordpress(
        open_api_key,
        wordpress_blog_url,
        wordpress_username,
        wordpress_password,
    )
    title = generator.generate_post_title(topic)
    content = generator.generate_post(title, tone, max_words)

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
    ) as progress:
        progress.add_task(description="Creating WordPress post...", total=None)
        generator.create_wordpress_post(title, content)
    rich.print(f"Created post with title: {title}")


if __name__ == '__main__':
    rich.print("\n")
    rich.print("█▀▀ █▀█ ▀█▀ ▄▄ ▀▀█   █░█░█ █▀█ █▀█ █▀▄ █▀█ █▀█ █▀▀ █▀ █▀   █▀█ █▀█ █▀ ▀█▀  █▀▀ █▀▀ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ █▀█ █▀█")
    rich.print("█▄█ █▀▀ ░█░ ░░ ▄██   ▀▄▀▄▀ █▄█ █▀▄ █▄▀ █▀▀ █▀▄ ██▄ ▄█ ▄█   █▀▀ █▄█ ▄█ ░█░  █▄█ ██▄ █░▀█ ██▄ █▀▄ █▀█ ░█░ █▄█ █▀▄")

    typer.run(cli)
