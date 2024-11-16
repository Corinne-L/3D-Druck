output_filename = ("TEST_Output")



save_xyz(output_filename, filtered_points)


    # Output speichern und bereitstellen
        st.write(f"Gefilterte Punkte: {filtered_points.shape[0]}")
        if st.button("Download gefilterter Punktwolke"):
            csv = "\n".join(" ".join(map(str, row)) for row in filtered_points)
            st.download_button(
                label="Gefilterte Punktwolke herunterladen",
                data=csv,
                file_name="filtered_output.xyz",
                mime="text/plain",
            )

    except Exception as e:
        st.error(f"Fehler: {e}")

