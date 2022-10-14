"""
Module for converting DEM to spectral cube
"""
import ndcube
import numpy as np
import astropy.units as u
from synthesizAR.atomic.idl import read_spectral_table, compute_spectral_table

__all__ = ['SpectralModel']


class SpectralModel:

    def __init__(self, spectral_table=None, **kwargs):
        if spectral_table is None:
            # compute spectral table
            self.spectral_table = self.build_spectral_table()
        elif isinstance(spectral_table, ndcube.NDCube):
            self.spectral_table = spectral_table
        else:
            self.spectral_table = read_spectral_table(spectral_table)

    @staticmethod
    def build_spectral_table(**kwargs):
        """
        Build the spectral table with some sensible defaults for MOXSI
        """
        temperature = kwargs.pop('temperature', np.arange(5.5, 7.6, 0.1)*u.K)
        density = kwargs.pop('density', None)
        if density is None:
            # Assume constant pressure
            pressure = 1e15 * u.cm**(-3) * u.K
            density = pressure / temperature
        wave_min = kwargs.pop('wave_min', 0.5 * u.angstrom)
        wave_max = kwargs.pop('wave_max', 60.5 * u.angstrom)
        delta_wave = kwargs.pop('delta_wave', 25 * u.milliangstrom)
        ioneq_filename = kwargs.pop('ioneq_filename', 'chianti.ioneq')
        abundance_filename = kwargs.pop('abundance_filename', 'sun_coronal_1992_feldman.abund')
        ion_list = kwargs.pop('ion_list', None)
        include_continuum = kwargs.pop('include_continuum', True)
        chianti_dir = kwargs.pop('chianti_dir', None)
        return compute_spectral_table(
            temperature,
            density,
            wave_min,
            wave_max,
            delta_wave,
            ioneq_filename,
            abundance_filename,
            ion_list=ion_list,
            include_continuum=include_continuum,
            chianti_dir=chianti_dir,
        )