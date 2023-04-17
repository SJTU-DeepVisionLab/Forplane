from lerplanes.utils.parse_args import parse_optfloat
from lerplanes.utils.create_rendering import render_to_path, decompose_space_time, render_to_path_with_pointcloud
<<<<<<< HEAD
from lerplanes.runners import static_trainer
from lerplanes.runners import phototourism_trainer
=======
>>>>>>> b26eda0cef18828bb6d35a349459deb84f752fbb
from lerplanes.runners import video_trainer
import torch.utils.data
import torch
import argparse
import importlib.util
import logging
import os
import pprint
import sys
from typing import List, Dict, Any
import tempfile
import numpy as np

import random


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = True


def get_freer_gpu():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_fname = os.path.join(tmpdir, "tmp")
        os.system(
            f'nvidia-smi -q -d Memory |grep -A5 GPU|grep Free >"{tmp_fname}"')
        if os.path.isfile(tmp_fname):
            memory_available = [int(x.split()[2])
                                for x in open(tmp_fname, 'r').readlines()]
            if len(memory_available) > 0:
                return np.argmax(memory_available)
    # The grep doesn't work with all GPUs. If it fails we ignore it.
    return None


gpu = get_freer_gpu()
if gpu is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)
    print(f"CUDA_VISIBLE_DEVICES set to {gpu}")
else:
    print(f"Did not set GPU.")


def setup_logging(log_level=logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(level=log_level,
                        format='%(asctime)s|%(levelname)8s| %(message)s',
                        handlers=handlers,
                        force=True)


<<<<<<< HEAD
def load_data(model_type: str, data_downsample, data_dirs, validate_only: bool, render_only: bool, **kwargs):
    data_downsample = parse_optfloat(data_downsample, default_val=1.0)

    if model_type == 'endovideo':
        return video_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, **kwargs)
    elif model_type == "video":
        return video_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, **kwargs)
    elif model_type == "phototourism":
        return phototourism_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, **kwargs
        )
    else:
        return static_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, **kwargs)


def init_trainer(model_type: str, **kwargs):
    if model_type == "video":
        from lerplanes.runners import video_trainer
        return video_trainer.VideoTrainer(**kwargs)
    elif model_type == "endovideo":
        from lerplanes.runners import video_trainer
        # in fact, endo dataset still uses video trainer.
        return video_trainer.VideoTrainer(**kwargs)
    elif model_type == "phototourism":
        from lerplanes.runners import phototourism_trainer
        return phototourism_trainer.PhototourismTrainer(**kwargs)
    else:
        from lerplanes.runners import static_trainer
        return static_trainer.StaticTrainer(**kwargs)
=======
def load_data(data_downsample, data_dirs, validate_only: bool, render_only: bool, **kwargs):
    data_downsample = parse_optfloat(data_downsample, default_val=1.0)

    return video_trainer.load_data(
        data_downsample, data_dirs, validate_only=validate_only,
        render_only=render_only, **kwargs)


def init_trainer(**kwargs):
    from lerplanes.runners import video_trainer
    return video_trainer.VideoTrainer(**kwargs)
>>>>>>> b26eda0cef18828bb6d35a349459deb84f752fbb


def save_config(config):
    log_dir = os.path.join(config['logdir'], config['expname'])
    os.makedirs(log_dir, exist_ok=True)

    with open(os.path.join(log_dir, 'config.py'), 'wt') as out:
        out.write('config = ' + pprint.pformat(config))

    with open(os.path.join(log_dir, 'config.csv'), 'w') as f:
        for key in config.keys():
            f.write("%s\t%s\n" % (key, config[key]))


def main():
    setup_logging()

    p = argparse.ArgumentParser(description="")

    p.add_argument('--render-only', action='store_true')
    p.add_argument('--validate-only', action='store_true')
    p.add_argument('--spacetime-only', action='store_true')
    p.add_argument('--save-train-time-step', action='store_true')
    p.add_argument('--config-path', type=str, required=True)
    p.add_argument('--log-dir', type=str, default=None)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('override', nargs=argparse.REMAINDER)

    args = p.parse_args()

    # Set random seed
    seed_everything(args.seed)

    # Import config
    spec = importlib.util.spec_from_file_location(
        os.path.basename(args.config_path), args.config_path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    config: Dict[str, Any] = cfg.config
    # Process overrides from argparse into config
    # overrides can be passed from the command line as key=value pairs. E.g.
    # python lerplanes/main.py --config-path lerplanes/config/cfg.py max_ts_frames=200
    # note that all values are strings, so code should assume incorrect data-types for anything
    # that's derived from config - and should not a string.
    overrides: List[str] = args.override
    overrides_dict = {ovr.split("=")[0]: ovr.split("=")[
        1] for ovr in overrides}
    config.update(overrides_dict)
    config['batch_size'] = int(config['batch_size'])
    config['num_steps'] = int(config['num_steps'])
<<<<<<< HEAD
    if "keyframes" in config:
        if 'endo' in config:
            model_type = 'endovideo'
        else:
            model_type = "video"
    elif "appearance_embedding_dim" in config:
        model_type = "phototourism"
    else:
        model_type = "static"
=======
>>>>>>> b26eda0cef18828bb6d35a349459deb84f752fbb
    validate_only = args.validate_only
    render_only = args.render_only
    spacetime_only = args.spacetime_only
    if validate_only and render_only:
        raise ValueError(
            "render_only and validate_only are mutually exclusive.")
    if render_only and spacetime_only:
        raise ValueError(
            "render_only and spacetime_only are mutually exclusive.")
    if validate_only and spacetime_only:
        raise ValueError(
            "validate_only and spacetime_only are mutually exclusive.")

    assert not('mask' in config and 'maskIS' in config)

    pprint.pprint(config)
    if validate_only or render_only:
        if args.log_dir is None:
            args.log_dir = os.path.join(config['logdir'], config['expname'])
        print('log_dir:', args.log_dir)
        assert args.log_dir is not None and os.path.isdir(args.log_dir)
    else:
        save_config(config)

<<<<<<< HEAD
    data = load_data(model_type, validate_only=validate_only,
                     render_only=render_only or spacetime_only, **config)
    config.update(data)
    trainer = init_trainer(model_type, **config)
=======
    data = load_data(validate_only=validate_only,
                     render_only=render_only or spacetime_only, **config)
    config.update(data)
    trainer = init_trainer(**config)
>>>>>>> b26eda0cef18828bb6d35a349459deb84f752fbb

    if args.log_dir is None and os.path.exists(os.path.join(config['logdir'], config['expname'], "model.pth")):
        args.log_dir = os.path.join(config['logdir'], config['expname'])

<<<<<<< HEAD
    if args.log_dir is not None:
        checkpoint_path = os.path.join(args.log_dir, "model.pth")
        is_training = not (validate_only or render_only or spacetime_only)
        trainer.load_model(torch.load(checkpoint_path), is_training=is_training)

    if validate_only:
        # if config['endo'] == True:
        #     trainer.validate_endo()
        trainer.validate()
    elif render_only:
        if 'endo' in config:
            render_to_path_with_pointcloud(trainer)
        else:
            render_to_path(trainer, extra_name="")
=======
    # always train a new model
    # if args.log_dir is not None:
    #     checkpoint_path = os.path.join(args.log_dir, "model.pth")
    #     is_training = not (validate_only or render_only or spacetime_only)
    #     trainer.load_model(torch.load(checkpoint_path), is_training=is_training)

    if validate_only:
        trainer.validate()
    elif render_only:
        render_to_path_with_pointcloud(trainer)
>>>>>>> b26eda0cef18828bb6d35a349459deb84f752fbb
    elif spacetime_only:
        decompose_space_time(trainer, extra_name="")
    elif args.save_train_time_step:
        trainer.train_with_time_step_saving(trainer) 
    else:
        trainer.train()
<<<<<<< HEAD
        if 'endo' in config:
            render_to_path_with_pointcloud(trainer)
=======
        render_to_path_with_pointcloud(trainer)
>>>>>>> b26eda0cef18828bb6d35a349459deb84f752fbb


if __name__ == "__main__":
    main()
