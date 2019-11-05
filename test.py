def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 100


def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 60


def test_forms(cldf_dataset):
    f = [
        f for f in cldf_dataset["FormTable"] if f["Value"] == 'iɾu [m], iɾutiɾa [f]'
    ]
    assert len(f) == 2

    assert f[0]["Parameter_ID"] == "5_that"
    assert f[0]["Language_ID"] == "Yawalapiti"
    assert f[0]["Form"] == "iɾu"

    assert f[1]["Parameter_ID"] == "5_that"
    assert f[1]["Language_ID"] == "Yawalapiti"
    assert f[1]["Form"] == "iɾutiɾa"

