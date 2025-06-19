{pkgs ? import <nixpkgs> {}}:
(pkgs.buildFHSEnv {
  name = "python-uv";
  targetPkgs = pkgs: (with pkgs; [
    gcc
    python313
    uv
  ]);
  runScript = "zeditor .";
  UV_PYTHON_DOWNLOADS = "never";
}).env
