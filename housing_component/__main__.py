import uvicorn
from housing_component.settings import AUTO_RELOAD


def main() -> None:
    uvicorn.run(
        app="housing_component.app:app",
        host="0.0.0.0",
        port=9103,
        reload=AUTO_RELOAD,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
