# AI Storyteller - Web application to generate and present stories
![image](https://github.com/Jorineg/AI-Story-Teller/assets/65853883/74207a8a-7574-4601-99b6-4bc106aa4d23)

See live demo at https://jorin.createuky.net/

This is a Flask based server that generates a story based on a given prompt or title.
To present the story in an interesting way, stable diffusion is used to generate images that fit the story and the elevenlabs API is used to narrate the story.

The story is generated in multiple steps:
- Draft different idas
- Rate ideas and choose best
- Generate characters and other story metadata
- Generate headlines for chapters
- Write the chapters
- Generate image prompt and image for each chapter
- Use elevenlabs to create audio for each chapter
