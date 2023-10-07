from src.vision.level_scanner import LevelScanner


def test_data_recorder():
    done = set([x for x in """
        test_images/Screenshot_20220521-095946.png	__________
        test_images/Screenshot_20220521-100008.png	__X_____X_
        test_images/Screenshot_20220521-100626.png	_XX___X_
        test_images/Screenshot_20220521-100140.png	XXXXX_X_XX
        test_images/Screenshot_20220521-100154.png	XXXXXXX_XX
        test_images/Screenshot_20220521-100022.png	X_X_____X_
    """.split() if "test_images" in x])
    print(done)
    from os import walk
    path = "test_images/"
    filenames = next(walk(path), (None, None, []))[2]  # [] if no file
    images = [path + filename for filename in filenames]
    data = []
    for image in images:
        if image in done:
            continue
        try:
            render(cv2.imread(image))
        except:
            continue
        rpr = input()
        print(f"{image}\t{rpr}")
        data.append((image, rpr))

    print(data)
    for d in data:
        print(d)


def run_level_scanner_tests():
    test_data = """('test_images/Screenshot_20220521-095946.png', '__________')
    ('test_images/Screenshot_20220521-100008.png', '__X_____X_')
    ('test_images/Screenshot_20220521-100626.png', '_XX___X_')
    ('test_images/Screenshot_20220521-100140.png', 'XXXXX_X_XX')
    ('test_images/Screenshot_20220521-100154.png', 'XXXXXXX_XX')
    ('test_images/Screenshot_20220521-100022.png', 'X_X_____X_')
    ('test_images/Screenshot_20220521-095834.png', '______')
    ('test_images/Screenshot_20220521-100755.png', 'XXX _XX_XXX')
    ('test_images/Screenshot_20220521-095639.png', '_XXXXX')
    ('test_images/Screenshot_20220521-100651.png', '___ _______')
    ('test_images/Screenshot_20220521-100453.png', 'XXXXX__X XXX_')
    ('test_images/Screenshot_20220521-100056.png', 'X_X_X___XX')
    ('test_images/Screenshot_20220521-095924.png', 'X____')
    ('test_images/Screenshot_20220521-095933.png', 'XX___')
    ('test_images/Screenshot_20220521-100333.png', '________ ____')
    ('test_images/Screenshot_20220521-100441.png', 'X_XXX__X XXX_')
    ('test_images/Screenshot_20220521-095711.png', '______')
    ('test_images/Screenshot_20220521-100640.png', 'XXXX_XX_')
    ('test_images/Screenshot_20220521-100127.png', 'XXXXX_X_XX')
    ('test_images/Screenshot_20220521-101205.png', '_XX_')
    ('test_images/Screenshot_20220521-100117.png', 'XXX_X_X_XX')
    ('test_images/Screenshot_20220521-095520.png', '_X____')
    ('test_images/Screenshot_20220521-100507.png', 'XXXXXX_X XXXX')
    ('test_images/Screenshot_20220521-095911.png', '_____')
    ('test_images/Screenshot_20220521-101009.png', '_____')
    ('test_images/Screenshot_20220521-095902.png', '_____')
    ('test_images/Screenshot_20220521-100931.png', '___XX___X_')
    ('test_images/Screenshot_20220521-095726.png', '_X__XX')
    ('test_images/Screenshot_20220521-100700.png', 'XXX _X__X_X')
    ('test_images/Screenshot_20220521-095813.png', 'XX_XXX')
    ('test_images/Screenshot_20220521-100405.png', 'X_XXX__X X___')
    ('test_images/Screenshot_20220521-101055.png', 'X___')
    ('test_images/Screenshot_20220521-101042.png', '____')
    ('test_images/Screenshot_20220521-100349.png', 'X_XX___X X___')
    ('test_images/Screenshot_20220521-095540.png', '_XXX__')
    ('test_images/Screenshot_20220521-101137.png', '_X__')
    ('test_images/Screenshot_20220521-100946.png', '_________')
    ('test_images/Screenshot_20220521-095800.png', 'XX__XX')
    ('test_images/Screenshot_20220521-100600.png', '________')
    ('test_images/Screenshot_20220521-101244.png', '__________')
    ('test_images/Screenshot_20220521-095551.png', '_XXX_X')
    ('test_images/Screenshot_20220521-101126.png', '____')
    ('test_images/Screenshot_20220521-100038.png', 'X_X_____XX')
    ('test_images/Screenshot_20220521-100825.png', '_______')
    ('test_images/Screenshot_20220521-100616.png', '_XX_____')"""

    test_data = [eval(x.strip()) for x in test_data.split("\n")]
    print(f"Number of tests: {len(test_data)}")
    for entry in test_data:
        image_file, expected_level = entry
        actual_level = LevelScanner().scan_from_path(image_file)
        assert actual_level == expected_level, f"{actual_level}, {expected_level}, {image_file}"
    print("All tests passed")


if __name__ == '__main__':
    run_level_scanner_tests()
