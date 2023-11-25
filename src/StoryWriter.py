from Scheduler import Scheduler
import traceback
import copy


from ApiConnector import (
    generate_next_paragraph,
    generate_audio,
    generate_image,
    generate_stable_diffusion_prompt,
    generate_character_details,
    generate_story_ideas,
    choose_story_idea,
    validate_query,
    generate_story_json,
    generate_paragraph_headings,
    generate_image_json,
)

from Storage import (
    find_stored_story_by_id,
    store_story_baseline,
    store_story,
    store_story_ending,
    store_text_illustration,
    update_stored_story,
    create_story_folder,
    store_story_thumbnail,
)

from config import prompt_params
import logging

logger = logging.getLogger(__name__)


def create_new_story(query, story_id):
    storage = {}
    store = lambda key, value: storage.update({key: value})
    load = lambda key: copy.deepcopy(storage.get(key))

    store("query", query)
    store("story_id", story_id)

    def on_generation_error(error):
        story = find_stored_story_by_id(story_id)
        story["generation_level"] = -1
        story["error"] = {
            "type": "generation error",
            "message": str(error),
            "traceback": traceback.format_exc(),
        }
        update_stored_story(story)

    scheduler = Scheduler(store, load, on_error=on_generation_error)

    def check_validation(query_valid):
        if query_valid == "y":
            return True
        else:
            story = find_stored_story_by_id(story_id)
            story["generation_level"] = -1
            story["error"] = {
                "type": "content filter triggered",
                "message": "",
            }
            update_stored_story(story)
            logger.error("Content filter triggered")
            return None

    scheduler.addTask(
        validate_query,
        ["query"],
        "query_valid",
    )

    scheduler.addTask(
        check_validation,
        ["query_valid"],
        "ready_to_start",
    )

    scheduler.addTask(
        create_story_folder,
        ["story_id", "ready_to_start"],
    )

    scheduler.addTask(
        generate_story_ideas,
        ["ready_to_start", "query"],
        "story_ideas",
    )

    scheduler.addTask(
        choose_story_idea,
        ["story_ideas", "query"],
        "story_summary",
    )

    def add_character_details_task(character, place, time):
        name = character["name"]
        store("character_infos_" + name, character)
        store("story_place", place)
        store("story_time", time)
        scheduler.addTask(
            generate_character_details,
            ["story_summary", f"character_infos_{name}", "story_place", "story_time"],
            f"character_details_{name}",
        )

    scheduler.addTask(
        generate_story_json,
        ["query", "story_summary"],
        "story_json",
        incremental=add_character_details_task,
    )

    scheduler.addTask(
        lambda _: 0,
        ["ready_to_start"],
        "section_nr",
    )

    scheduler.addTask(
        store_story_baseline,
        ["story_json", "story_id"],
    )

    scheduler.addTask(
        store_story_thumbnail,
        ["story_id", "illustration_ready_1"],
    )

    def store_story_title_and_summary(story_id, story_json, story_summary):
        story = find_stored_story_by_id(story_id)
        story["title"] = story_json["title"]
        story["summary"] = story_summary
        update_stored_story(story)

    scheduler.addTask(
        store_story_title_and_summary,
        ["story_id", "story_json", "story_summary"],
    )

    scheduler.addTask(
        generate_paragraph_headings,
        ["story_json", "story_summary"],
        "paragraph_headings",
    )

    store("previous_paragraphs_1", [])
    store("paragraph_0", "")

    def add_paragraph_tasks(paragraph_headings, story_json):
        character_details = [
            f"character_details_{x['name']}" for x in story_json["characters"]
        ]

        scheduler.addTask(
            store_story,
            [
                "story_id",
                *[f"paragraph_{i}" for i in range(1, len(paragraph_headings) + 1)],
            ],
        )

        for paragraph_number in range(1, len(paragraph_headings) + 1):

            def paragraph_generation_callback(
                paragraph, f_paragraph_number=paragraph_number
            ):
                previous_paragraphs = load(f"previous_paragraphs_{f_paragraph_number}")
                previous_paragraphs.append(paragraph)
                store(
                    f"previous_paragraphs_{f_paragraph_number+1}", previous_paragraphs
                )

            scheduler.addTask(
                lambda *args, p_nr=paragraph_number: generate_next_paragraph(
                    p_nr, *args
                ),
                [
                    "story_json",
                    "paragraph_headings",
                    f"previous_paragraphs_{paragraph_number}",
                    *character_details,
                ],
                f"paragraph_{paragraph_number}",
                callback=paragraph_generation_callback,
            )

            scheduler.addTask(
                generate_image_json,
                [
                    "paragraph_1",
                    f"paragraph_{paragraph_number-1}",
                    f"paragraph_{paragraph_number}",
                    "story_json",
                ],
                f"image_json_{paragraph_number}",
            )

            scheduler.addTask(
                generate_stable_diffusion_prompt,
                [f"image_json_{paragraph_number}", "story_json", *character_details],
                f"image_prompt_{paragraph_number}",
            )

            scheduler.addTask(
                lambda *args, p_nr=paragraph_number: generate_image(p_nr, *args),
                [f"image_prompt_{paragraph_number}", "story_id", "story_json"],
                f"illustration_ready_{paragraph_number}",
            )

            scheduler.addTask(
                lambda *args, p_nr=paragraph_number: generate_audio(
                    story_json["audio_narrator"], p_nr, *args
                ),
                [f"paragraph_{paragraph_number}", "story_id"],
                f"audio_ready_{paragraph_number}",
            )

            def update_generation_level(*_, f_paragraph_number=paragraph_number):
                story = find_stored_story_by_id(story_id)
                story["generation_level"] = f_paragraph_number + 1
                update_stored_story(story)
                return True

            previsous_section_ready = [f"section_ready_{paragraph_number - 1}"]
            scheduler.addTask(
                update_generation_level,
                [
                    f"illustration_ready_{paragraph_number}",
                    f"audio_ready_{paragraph_number}",
                ]
                + previsous_section_ready,
                f"section_ready_{paragraph_number}",
            )

    scheduler.addTask(
        add_paragraph_tasks,
        ["paragraph_headings", "story_json"],
    )

    def generate_first_view(story_id, story_json):
        title_text_illustration = {
            "text": story_json["title"],
            "text_color": story_json["title_font_color"],
            "bg_color": story_json["title_background_color"],
            "font": story_json["title_font_family"],
        }
        store_text_illustration(0, title_text_illustration, story_id)
        scheduler.addTask(
            lambda b, id: generate_audio(b["audio_narrator"], 0, b["title"], id),
            ["story_json", "story_id"],
            f"audio_ready_0",
        )
        return True

    scheduler.addTask(
        generate_first_view,
        ["story_id", "story_json"],
        "illustration_ready_0",
    )

    scheduler.addTask(
        lambda *_: True,
        ["illustration_ready_0", "audio_ready_0"],
        "section_ready_0",
    )

    scheduler.addTask(
        store_story_ending,
        ["section_nr", "story_id", "story"],
    )

    def store_generation_level_completed(*_):
        story = find_stored_story_by_id(story_id)
        story["generation_level"] = load("section_nr") + 2
        update_stored_story(story)
        return True

    def add_generation_level_completed_task(_):
        last_section_nr = load("section_nr")
        scheduler.addTask(
            store_generation_level_completed,
            [f"section_ready_{last_section_nr}"],
            "story_generation_completed",
        )

    scheduler.addTask(
        add_generation_level_completed_task,
        ["story"],
    )
