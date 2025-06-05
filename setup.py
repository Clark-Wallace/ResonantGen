from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resonantgen",
    version="0.1.0",
    author="ResonantGen Team",
    author_email="contact@resonantgen.ai",
    description="AI Music Workstation - Natural language music generation with selective track regeneration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ResonantGen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "transformers>=4.30.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "gradio>=3.0.0",
        "numpy>=1.21.0",
        "librosa>=0.10.0",
        "scipy>=1.9.0",
        "pydantic>=2.0.0",
        "pydub>=0.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "performance": [
            "xformers>=0.0.20",
            "flash-attn>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "resonantgen=resonantgen.cli:main",
            "resonantgen-server=resonantgen.api.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)