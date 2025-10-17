from main.artificial_pancreas import ArtificialPancreasSystem
import pytest


@pytest.fixture
def artificial_pancreas():
    return ArtificialPancreasSystem(100.0)
    
    
def test_glucose_increases_after_meal(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.meal(20.0)
    assert artificial_pancreas.glucose_level == 110.0
    

def test_glucose_never_below_min(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.exercise(200.0) #glucose burn should be 60, glucose level drops to 40
    assert artificial_pancreas.glucose_level == 50.0
    

def test_glucose_decreases_after_excercise(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.exercise(60.0)
    assert artificial_pancreas.glucose_level == 82.0
    
def test_deliver_insulin(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.meal(100.0)
    result = artificial_pancreas.predict_action()
    assert result == ('deliver_insulin', 100.0)
    

def test_warn_low_glucose(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.exercise(200.0)
    result = artificial_pancreas.predict_action()
    assert result == ('warn_low_glucose', 50.0)
    
    
def test_maintain(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.meal(10.0)
    result = artificial_pancreas.predict_action()
    assert result == ('maintain', 105.0)
    
    
def test_sequential_events(artificial_pancreas: ArtificialPancreasSystem):
    artificial_pancreas.meal(30.0) #increases glucose_level to 115
    assert artificial_pancreas.glucose_level == 115.0

    artificial_pancreas.exercise(50.0) #decreases glucose_level back to 100
    assert artificial_pancreas.glucose_level == 100.0
    
    artificial_pancreas.meal(100.0) #increases glucose_level to 150
    assert artificial_pancreas.glucose_level == 150.0
    
    result = artificial_pancreas.predict_action()
    assert result == ('deliver_insulin', 100.0)
    
    result = artificial_pancreas.predict_action()
    assert result == ('maintain', 100.0)
    
    artificial_pancreas.exercise(60.0) #decreases glucose_level to 82
    result = artificial_pancreas.predict_action()
    assert result == ('warn_low_glucose', 82.0)
    
    
def test_exceptions():
    with pytest.raises(TypeError):
        ArtificialPancreasSystem('abc')
    
    with pytest.raises(ValueError):
        ArtificialPancreasSystem(-100.0)
        
    with pytest.raises(TypeError):
        ArtificialPancreasSystem(100.0).meal('abc')
        
    with pytest.raises(ValueError):
        ArtificialPancreasSystem(100.0).meal(-100.0)
        
    with pytest.raises(TypeError):
        ArtificialPancreasSystem(100.0).exercise('abc')
        
    with pytest.raises(ValueError):
        ArtificialPancreasSystem(100.0).exercise(-100.0)


 
    


    
    


    
    
    
    