from app import add, sub, mul, div
def test_add():
    result=add(2,3)
    assert result==5
def test_sub():
    result=sub(5,2)
    assert result==3    

def test_mul():
    result=mul(2,3)
    assert result==6
def test_div():
    result=div(6,2)
    assert result==3