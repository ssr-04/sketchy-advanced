{ pkgs }: {
  deps = [pkgs.strace

  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      # Needed for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
      # Needed for matplotlib
      pkgs.xorg.libX11
      # Needed for opencv-python
      pkgs.libGL
      pkgs.xorg.libxcb
      pkgs.xorg.libSM
      pkgs.xorg.libICE
    ];
  };
}