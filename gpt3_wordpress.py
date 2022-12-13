import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost


class Gpt3Wordpress:
    def __init__(self, api_key, blog_url, username, password):
        openai.api_key = api_key
        self.blog_url = blog_url
        self.username = username
        self.password = password

    def generate_post_title(self, topic: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Provide the idea for a new blog post in form of title. "
                   f"The blog post title should be about {topic}."
                   f"Post's title length must be between 50 and 70 characters.",
            temperature=0.6,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        return response.choices[0].text

    def generate_post(self, title: str, tone: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Provide the content for a new blog post. "
                   f"The blog post should be about {title}."
                   f"Tone of the post should be {tone}."
                   f"Post's content length should be between 2000 and 2500 words.",
            temperature=0.6,
            max_tokens=3000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        return response.choices[0].text

    def create_wordpress_post(self, title, content):
        client = Client(self.blog_url, self.username, self.password)
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'draft'
        client.call(NewPost(post))


