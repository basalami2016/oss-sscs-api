{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixpkgs-unstable;  
    fh.url = "https://api.flakehub.com/f/DeterminateSystems/fh/0.1.*.tar.gz";  
  };
  outputs = { self, nixpkgs, fh, } @ inputs:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {      
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {       
      packages = forEachSupportedSystem ({ pkgs }: {
        # alias pkgs.python3Packages pointing to pkgs.python311Packages
        default =
          let            
            #python = pkgs.python311;
          in 
            #A derivation is a function (e.g. python.pkgs.buildPythonApplication rec) describes a build process
            #alias pkgs.python3Packages pointing to pkgs.python311Packages
            #buildPythonApplication function is used to build a Python package where one is interested only in the executables and not importable modules
            pkgs.python3Packages.buildPythonApplication rec{ 
              name = "software-supply-chain-security";
              version = "0.0.1";
              pyproject = true;          
              src = ./.;

              #dependencies is specifyied in buildInputs and propagatedBuildInputs 
              #build-time dependency should be included in buildInputs
              #runtime dependency should be added to propagatedBuildInputs
              #Test dependencies are considered build-time dependencies and passed to nativeCheckInputs
              buildInputs = with pkgs.python3Packages; [ 
                pyramid                            
              ];

              #Build-time only dependencies - items listed in setup_requires
              nativeBuildInputs = with pkgs.python3Packages; [
                 setuptools
                 wheel
              ];

              #Items listed in install_requires go here
              propagatedBuildInputs = with pkgs.python3Packages; [                
                 #asyncio
                 #logging 
                 pkgs.python311Packages.aiofiles     
                 pkgs.python311Packages.aiocron                   
                 pkgs.python311Packages.aioazuredevops 
                 pkgs.python311Packages.requests   
              ];
            };                
      });

      devShells = forEachSupportedSystem ({ pkgs}: {
        default =
          let
            # Use Python 3.11
            #python = pkgs.python311;
            pythonPackages = pkgs.python3Packages;  
            name = "impurePythonEnv";
            venvDir = "./.venv";            
          in
           pkgs.mkShell{   

             #name = "impurePythonEnv";
             #venvDir = "./.venv";  

             buildInputs = with pkgs.python3Packages; [ 
               pkgs.python3Packages.python  
               pkgs.python3Packages.venvShellHook             
             ];    
           
             # The Nix packages provided in the environment
             packages = with pkgs; 
              [
                # Python plus helper tools
                (python3.withPackages (ps: with ps; [
                  virtualenv # Virtualenv
                  pip # The pip installer                 
                ]))
              ] ++
              [
                # Go helper tools
                go 
                gopls 
                gotools 
                go-tools 
              ] ++             
              [                
                trivy
                grype
                syft
                osv-scanner
                cdxgen
                docker
              ]++
              [
               maven
              ];            
              GREETING = "OSS Scanning apps";               
              shellHook = ''
                 echo $GREETING 
              ''; 

              # Run this command, only after creating the virtual environment
              postVenvCreation = ''
                 unset SOURCE_DATE_EPOCH
                 pip install -r requirements.txt
              '';
          };        
      });
    };
}





















