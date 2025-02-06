{
  description = "";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.11";
    unstable.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs, unstable }: 
  let
    system = "x86_64-linux";
  in
  {
    nixosConfigurations = {
      desktop = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [ 
	  ./configuration.nix 
	  ./hosts/desktop.nix 
	  ./modules/nvidia
        ];
      };
      laptop = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [ 
	  ./configuration.nix 
	  ./hosts/laptop.nix 
	  ./modules/nvidia
        ];
      };
      thinkpad = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [ 
	  ./configuration.nix 
	  ./hosts/thinkpad.nix 
        ];
      };
    };
  };
}
