export CUDA_VISIBLE_DEVICES=0

PYTHONPATH='.' python lerplanes/main.py --config-path lerplanes/configs/final/endonerf/aba_loss_var/no_planetv/full_2000_cutting.py --validate-only
PYTHONPATH='.' python lerplanes/main.py --config-path lerplanes/configs/final/endonerf/aba_loss_var/no_planetv/full_2000_pulling.py --validate-only
PYTHONPATH='.' python lerplanes/main.py --config-path lerplanes/configs/final/endonerf/aba_loss_var/no_planetv/full_2000_pushing.py --validate-only
PYTHONPATH='.' python lerplanes/main.py --config-path lerplanes/configs/final/endonerf/aba_loss_var/no_planetv/full_2000_tearing.py --validate-only
PYTHONPATH='.' python lerplanes/main.py --config-path lerplanes/configs/final/endonerf/aba_loss_var/no_planetv/full_2000_thin.py --validate-only
PYTHONPATH='.' python lerplanes/main.py --config-path lerplanes/configs/final/endonerf/aba_loss_var/no_planetv/full_2000_traction.py --validate-only