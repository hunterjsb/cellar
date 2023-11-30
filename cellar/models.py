from dataclasses import dataclass, fields

from flask import Request


@dataclass
class FormData:
    threshold: int
    minsize: int
    maxsize: int
    scale: float
    offset: float
    px_nm: float

    @property
    def scale_factor_px2_per_nm2(self):
        return self.px_nm ** 2  # nm^2/px^2

    @classmethod
    def from_request(cls, request: Request):
        kwargs = {}
        for f in fields(cls):
            kwargs[f.name] = f.type(request.form[f.name])
        return cls(**kwargs)


if __name__ == '__main__':
    form = FormData(0, 1, 2, .1, .2, .3)
    for i in fields(form):
        print(i)
