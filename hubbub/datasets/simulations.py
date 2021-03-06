from datetime import datetime

# SIMPLE_LOG = [
#     (datetime(2000,  1,  1, 0,  1, 11)},
#     (datetime(2000,  1,  1, 0,  2, 49)},
#     (datetime(2000,  1,  1, 0,  3,  2)},
#     (datetime(2000,  1,  1, 0,  3, 28)},
#     (datetime(2000,  1,  1, 0, 13, 33)},
#     (datetime(2000,  1,  1, 0, 15, 57)},
#     (datetime(2000,  1,  1, 0, 16,  4)},
#     (datetime(2000,  1,  1, 0, 23, 36)},
#     (datetime(2000,  1,  1, 0, 24, 25)},
#     (datetime(2000,  1,  1, 0, 24, 40)},
#     ]

SIMPLE_LOG = [
    (datetime(2000,  1,  1, 0,  1,  1, 123456), 10),
    (datetime(2000,  1,  1, 0,  2,  9, 123456), 10),
    (datetime(2000,  1,  1, 0,  3,  2, 123456), 10),
    (datetime(2000,  1,  1, 0,  4,  8, 123456), 10),
    (datetime(2000,  1,  1, 0,  5,  3, 123456), 10),
    (datetime(2000,  1,  1, 0,  6,  7, 123456), 10),
    (datetime(2000,  1,  1, 0,  7,  4, 123456), 10),
    (datetime(2000,  1,  1, 0,  8,  6, 123456), 10),
    (datetime(2000,  1,  1, 0,  9,  5, 123456), 10),
    (datetime(2000,  1,  1, 0, 10,  0, 123456), 10),
    ]


from random import randrange, gauss


def simple_log(n=10, days=1):
    LOG = [
        (datetime(2000, 1, randrange(1, days+1), randrange(24),  randrange(60),  randrange(60), randrange(10**6)), 10)
        for i in range(n)
        ]
    LOG.sort()
    return LOG


def gauss_log(n=10, days=1):
    start = 1402042195.
    dates = dates = [gauss(mu=0.5, sigma=0.2) * 86400 + start for i in range(n)]

    LOG = [
        (datetime.fromtimestamp(start + d), 10)
        for d in dates
        ]
    LOG.sort()
    return LOG
