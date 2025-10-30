{
  description = "Python flake for Flask";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        app = pkgs.stdenv.mkDerivation rec {
          pname = "dev";
          version = "0.1.0";
          src = ./src;
          
          # TODO Add templates and such
          installPhase = ''
            mkdir -p $out/bin
            cp ./*.py $out/bin
            '';
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.python311
            pkgs.python311Packages.flask
            pkgs.python311Packages.pylint # linter
            pkgs.python311Packages.pylsp-mypy # lsp
          ];

          shellHook = ''
            python --version
          '';
        };
        apps.default = { 
          type = "app";
          program = "${self.packages.${system}.default}/bin/run";

        };

        packages.default = pkgs.writeShellApplication {
          name = "run";
          runtimeInputs = [
            pkgs.python311
            pkgs.python311Packages.flask
            # app
          ];
          # TODO add database initialization
          text = ''
          echo "Starting flask development server..."
          flask --app ${app}/bin/main run
          '';
          };
        # packages.default = app;
      }
    );
}
