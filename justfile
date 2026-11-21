
default:
    @just --list

install:
    mise install
    uv sync

dev:
    moon run root:dev

test:
    moon run root:test

lint:
    moon run root:lint

format:
    moon run root:format

format-check:
    moon run root:format-check

check:
    just lint
    just format-check
    just test
