from functools import cache, partial

from .shared import P3, Solution, neighbors_3d


def main(input_: list[str]) -> Solution:
    points = {P3(*map(int, p.split(","))) for p in input_}
    part1 = sum([exposed_faces(p, points) for p in points])
    part2 = exterior_faces(points)
    return Solution(part1, part2)


def exposed_faces(point: P3, points: set[P3]) -> int:
    neighbors = neighbors_3d(point)
    overlap = neighbors.intersection(points)
    return 6 - len(overlap)


def exterior_faces(points: set[P3]) -> int:
    start = P3(0, 0, 0)
    max_coord = max(max(points).to_tuple()) + 2
    in_boundary = partial(in_bounds, boundary_point=P3(max_coord, max_coord, max_coord))

    q = [start]
    visited = set()
    faces = 0
    while q:
        c = q.pop(0)
        visited.add(c)
        for adj in neighbors_3d(c):
            if not in_boundary(adj):
                continue
            if adj in points:
                faces += 1
                continue
            if adj in visited or adj in q:
                continue
            q.append(adj)
    return faces


@cache
def in_bounds(point: P3, boundary_point: P3) -> bool:
    a, b, c = boundary_point.to_tuple()
    x, y, z = point.to_tuple()
    return 0 <= x <= a and 0 <= y <= b and 0 <= z <= c
