import openai
import rich
import typer

from rich.progress import Progress, SpinnerColumn, TextColumn
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost


class Gpt3Wordpress:
    def __init__(self, api_key: str, blog_url: str, username: str, password: str):
        openai.api_key = api_key
        self.blog_url = blog_url + "/xmlrpc.php"
        self.username = username
        self.password = password

    def _gpt3_query(self, prompt: str) -> str:
        """Query the OpenAI GPT-3 API with the given prompt and return the response."""
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.6,
                max_tokens=3000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.6,
            )
            return response.choices[0].text
        except Exception() as e:
            rich.print(f"Error: {e}")
            exit(1)

    def _generate_loop(self, prompt: str, kind: str) -> str:
        """Generate a title or post until it meets the requirements."""
        while True:
            with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
            ) as progress:
                progress.add_task(description=f"Generating {kind}...", total=None)
                content = self._gpt3_query(prompt)
            rich.print(f"\nGenerated {kind}: {content}")
            confirm = typer.confirm(f"\nDo you like the generated {kind}?")
            if confirm:
                return content

    def generate_post_title(self, topic: str) -> str:
        """Generate a post title."""
        return self._generate_loop(f"Blog post title."
                                   f"Title must be about {topic}."
                                   f"Length must be maximum 70 characters",
                                   "title")

    def generate_post(self, title: str, tone: str, max_workds: int) -> str:
        """Generate a post."""
        return self._generate_loop(f"Blog post which titles {title}. "
                                   f"Tone must be {tone}. "
                                   f"Lenght must be maximum {max_workds} words.",
                                   "post")

    def create_wordpress_post(self, title: str, content: str) -> None:
        """Create a WordPress post."""
        client = Client(self.blog_url, self.username, self.password)
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'draft'
        try:
            created_post = client.call(NewPost(post))
            return created_post.link
        except Exception() as e:
            rich.print(f"Error: {e}")
            exit(1)

