BARKER_CODE = [
  [1,1,1,0,0,1,0],
  [1,1,1,0,0,1,0],
  [1,1,1,0,0,1,0],
  [0,0,0,1,1,0,1],
  [0,0,0,1,1,0,1],
  [1,1,1,0,0,1,0],
  [0,0,0,1,1,0,1],
]

CORRECT_TOP_LEFT_BARKER_CODE = {
  'value': BARKER_CODE,
  'top': 0,
  'left': 0,
}

CORRECT_TOP_RIGHT_BARKER_CODE = {
  'value': BARKER_CODE,
  'top': 0,
  'left': 69,
}

CORRECT_BOTTOM_LEFT_BARKER_CODE = {
  'value': BARKER_CODE,
  'top': 69,
  'left': 0,
}

CORRECT_BOTTOM_RIGHT_BARKER_CODE = {
  'value': BARKER_CODE,
  'top': 69,
  'left': 69,
}

CORRECT_DOLBY_LOGO = {
  'value': [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0,0,1,1,0],
    [0,1,1,1,0,0,0,0,1,1,1,0],
    [0,1,1,1,1,0,0,1,1,1,1,0],
    [0,1,1,1,1,0,0,1,1,1,1,0],
    [0,1,1,1,1,0,0,1,1,1,1,0],
    [0,1,1,1,1,0,0,1,1,1,1,0],
    [0,1,1,1,0,0,0,0,1,1,1,0],
    [0,1,1,0,0,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
  ],
  'top': 32,
  'left': 32,
}

CORRECT_DOLBY_ASCII = {
  # 'value': [
  #   [1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0],
  #   [1,0,0,0,1,0,0,0,0,1,0,0,1,1,1,0,0,0,1,1],
  #   [1,1,1,1,0,1,1,1,0,0,0,1,0,1,0,1,1,1,0,0],
  #   [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
  # ],
  'value': [
    [1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0],
    [1,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,1,1],
    [1,1,1,1,0,1,1,1,0,0,0,1,0,1,0,1,1,1,0,0],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
  ],
  'top': 44,
  'left': 56,
}

KNOWN_PATTERNS = [
  CORRECT_TOP_LEFT_BARKER_CODE,
  CORRECT_TOP_RIGHT_BARKER_CODE,
  CORRECT_BOTTOM_LEFT_BARKER_CODE,
  CORRECT_BOTTOM_RIGHT_BARKER_CODE,
  CORRECT_DOLBY_LOGO,
  CORRECT_DOLBY_ASCII,
]