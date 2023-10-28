from geometry.line import Line2D
from core.geometry.geometry_2d.point.point import Point2D


def main() -> None:
    """_"""
    line: Line2D = Line2D(Point2D(1, 1), Point2D(2, 2))

    print(line.to_string())


if __name__ == "__main__":
    main()
