# Test task for Sporttech LLC

    virtualenv .venv
    source .venv/bin/activate

    pip install -r requirements.txt

    python run.py --help
> usage: run.py <command> [options]

> positional arguments:
>   {schedule,parse,show}
>     schedule            parse periodically and store results to a file
>     parse               parse once and display results on screen
>     show                show the table from file

> optional arguments:
>   -h, --help            show this help message and exit

## Parse and display the table
    python run.py parse

## Parse continuously with interval
    python run.py schedule

## Show saved data
    python run.py show


Copy config.template.yaml to config.yaml. Add teams to the appropriate section