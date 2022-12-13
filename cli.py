import os
import typer
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from gpt3_wordpress import Gpt3Wordpress

gpt3wordpress_cli = typer.Typer()

generator = Gpt3Wordpress(
    os.getenv("OPENAI_API_KEY"),
    os.getenv("WORDPRESS_BLOG_URL"),
    os.getenv("WORDPRESS_USERNAME"),
    os.getenv("WORDPRESS_PASSWORD"),
)


@gpt3wordpress_cli.command()
def cli(
        topic: str = typer.Option(..., prompt="\nWhat is the topic of the post?", help="The topic of the post."),
        tone: str = typer.Option(..., prompt="What is the tone of the post?", help="The tone of the post. (e.g. funny, "
                                                                                   "serious, etc.)"),
):
    while True:
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
        ) as progress:
            progress.add_task(description="Generating title...", total=None)
            title = generator.generate_post_title(topic).strip('\n')
        rich.print(f"\nGenerated title: {title}")
        confirm = typer.confirm("Do you like the title?")
        if confirm:
            rich.print(f"Using this title: {title}")
            break

    while True:
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
        ) as progress:
            progress.add_task(description="Generating post...", total=None)
            content = generator.generate_post(title, tone)
        rich.print(f"Generated content: {content}")
        confirm = typer.confirm("Do you like the post content?")
        if confirm:
            rich.print(f"Using this content: {content}")
            break

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
    ) as progress:
        progress.add_task(description="Creating WordPress post...", total=None)
        generator.create_wordpress_post(title, content)
    rich.print(f"Created post with title: {title}")


if __name__ == '__main__':
    typer.run(cli)
