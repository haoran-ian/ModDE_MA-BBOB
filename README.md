## Install ModDE 0.0.3
Repostory link: [https://github.com/Dvermetten/ModDE](https://github.com/Dvermetten/ModDE)
```bash
git clone -b 0.0.3 https://github.com/Dvermetten/ModDE.git
cd ModDE
pip install -r requirements.txt
pip install .
```

## Run experiment
```bash
python src.py -n=$n -i=$i -b=saturate
```
where $n is how many dimesions of xopt are near to the boundaries, $i (from 0 to 49) indicates which set of weights and iids to be used when generating MA-BBOB'.