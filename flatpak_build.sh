#!/bin/sh


echo "building package...................."
flatpak-builder build io.github.unicornyrainbow.secrets.yml --force-clean
echo "making .flatpak file..............."
rm -rf repo
flatpak-builder --force-clean --repo=repo build io.github.unicornyrainbow.secrets.yml	
flatpak build-bundle repo secrets.flatpak io.github.unicornyrainbow.secrets
echo "installing........................"
flatpak remove --force-remove --delete-data --noninteractive -y secrets
flatpak-builder --user --install --force-clean build "io.github.unicornyrainbow.secrets.yml"