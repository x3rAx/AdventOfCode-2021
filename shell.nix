let
  # Pinned nixpkgs, deterministic. Last updated: 2021-02-12.
  #pkgs = import (fetchTarball("https://github.com/NixOS/nixpkgs/archive/a58a0b5098f0c2a389ee70eb69422a052982d990.tar.gz")) {};

  # Specific NixOS release version. This is not the channel and does not get updated along with it.
  pkgs = import (fetchTarball("https://github.com/NixOS/nixpkgs/archive/refs/tags/21.11.tar.gz")) {};

  # Rolling updates, not deterministic.
  #pkgs = import (fetchTarball("channel:nixpkgs-unstable")) {};
in pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    bashInteractive
  ];
  buildInputs = with pkgs; [
  ] ++ (with python3Packages; [
    black
    ipykernel
    numpy
    scipy
  ]);

  # Certain Rust tools won't work without this
  # This can also be fixed by using oxalica/rust-overlay and specifying the rust-src extension
  # See https://discourse.nixos.org/t/rust-src-not-found-and-other-misadventures-of-developing-rust-on-nixos/11570/3?u=samuela. for more details.
  #RUST_SRC_PATH = "${pkgs.rust.packages.stable.rustPlatform.rustLibSrc}";
}
