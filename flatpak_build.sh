#!/bin/sh


echo "building package...................."
flatpak-builder build io.github.unicorn.secrets.yml --force-clean
echo "making .flatpak file..............."
rm -rf repo
flatpak-builder --force-clean --repo=repo build io.github.unicorn.secrets.yml	
flatpak build-bundle repo secrets.flatpak io.github.unicorn.secrets
echo "installing........................"
flatpak remove --force-remove --delete-data --noninteractive -y secrets
flatpak-builder --user --install --force-clean build "io.github.unicorn.secrets.yml"