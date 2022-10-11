#!/bin/sh

clear
echo "##########################  building  package  ##########################"
flatpak-builder --force-clean --repo=repo build flatpak/io.github.unicornyrainbow.secrets.yml	
flatpak build-bundle repo secrets.flatpak io.github.unicornyrainbow.secrets
echo "#########################  deleting old pakage  #########################"
flatpak remove --force-remove --noninteractive -y secrets
echo "########################  installing new pakage  ########################"
flatpak-builder --user --install --force-clean build "flatpak/io.github.unicornyrainbow.secrets.yml"
