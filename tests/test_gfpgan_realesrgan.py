from PIL import Image

from sdkit import Context
from sdkit.filter import apply_filters
from sdkit.models import load_model

from common import (
    TEST_DATA_FOLDER,
    assert_images_same,
    run_test_on_multiple_devices,
)

EXPECTED_DIR = f"{TEST_DATA_FOLDER}/expected_images"

context = None


def setup_module():
    global context

    context = Context()
    context.test_diffusers = True


def test_gfpgan_model_loads():
    context.model_paths["gfpgan"] = "models/gfpgan/GFPGANv1.3.pth"
    load_model(context, "gfpgan")


def test_realesrgan_model_loads():
    context.model_paths["realesrgan"] = "models/realesrgan/RealESRGAN_x4plus.pth"
    load_model(context, "realesrgan")


def test_gfpgan_applies():
    img = Image.open(f"{TEST_DATA_FOLDER}/input_images/man-512x512.png")

    filtered_img = apply_filters(context, "gfpgan", img)
    assert filtered_img is not None
    assert len(filtered_img) == 1

    expected_image = Image.open(f"{EXPECTED_DIR}/filters/gfpgan.png")
    assert_images_same(filtered_img[0], expected_image, "test_gfpgan")


def test_gfpgan_works_on_multiple_devices():
    def task(context):
        context.model_paths["gfpgan"] = "models/gfpgan/GFPGANv1.3.pth"
        load_model(context, "gfpgan")

        img = Image.open(f"{TEST_DATA_FOLDER}/input_images/man-512x512.png")

        filtered_img = apply_filters(context, "gfpgan", img)
        assert filtered_img is not None
        assert len(filtered_img) == 1

    run_test_on_multiple_devices(task, devices=["cpu", "cuda:0"])


def test_realesrgan_applies():
    img = Image.open(f"{TEST_DATA_FOLDER}/input_images/man-512x512.png")

    filtered_img = apply_filters(context, "realesrgan", img)
    assert filtered_img is not None
    assert len(filtered_img) == 1

    expected_image = Image.open(f"{EXPECTED_DIR}/filters/realesrgan.png")
    assert_images_same(filtered_img[0], expected_image, "test_realesrgan")


def test_realesrgan_works_on_multiple_devices():
    def task(context):
        context.model_paths["realesrgan"] = "models/realesrgan/RealESRGAN_x4plus.pth"
        load_model(context, "realesrgan")

        img = Image.open(f"{TEST_DATA_FOLDER}/input_images/man-512x512.png")
        img = img.resize((64, 64))

        filtered_img = apply_filters(context, "realesrgan", img)
        assert filtered_img is not None
        assert len(filtered_img) == 1

    run_test_on_multiple_devices(task, devices=["cpu", "cuda:0"])


def test_gfpgan_and_realesrgan_work_together_on_multiple_devices():
    def task(context):
        context.model_paths["gfpgan"] = "models/gfpgan/GFPGANv1.3.pth"
        load_model(context, "gfpgan")

        context.model_paths["realesrgan"] = "models/realesrgan/RealESRGAN_x4plus.pth"
        load_model(context, "realesrgan")

        img = Image.open(f"{TEST_DATA_FOLDER}/input_images/man-512x512.png")

        filtered_img = apply_filters(context, "gfpgan", img)
        assert filtered_img is not None
        assert len(filtered_img) == 1

        filtered_img = filtered_img[0].resize((64, 64))

        filtered_img = apply_filters(context, "realesrgan", filtered_img)
        assert filtered_img is not None
        assert len(filtered_img) == 1

    run_test_on_multiple_devices(task, devices=["cpu", "cuda:0"])
