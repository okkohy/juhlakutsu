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
          src = ./.;
          
          # TODO Add templates and such
          installPhase = ''
            mkdir -p $out/src
            cp src/*.py $out/src
            cp main.py $out
            cp -r ./templates $out
            '';
        };
        commonPkgs = with pkgs; [
          python311
          python311Packages.flask
          sqlite
        ];
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            # pkgs.python311
            # pkgs.python311Packages.flask
            pkgs.python311Packages.pylint # linter
            pkgs.python311Packages.pylsp-mypy # lsp
            pkgs.python311Packages.black # formatter
          ] ++ commonPkgs;

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
            # app
          ] ++ commonPkgs;
          # TODO add database initialization
          text = ''
          echo "Starting flask development server..."
          flask run
          '';
          };
        # packages.default = app;
      }
    );
}
